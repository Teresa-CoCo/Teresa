use serde::{Deserialize, Serialize};
use base64::{engine::general_purpose, Engine as _};

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatRequest {
    pub api_url: String,
    pub api_key: String,
    pub model: String,
    pub messages: Vec<ChatMessage>,
}

#[tauri::command]
async fn ping_host(host: String) -> Result<String, String> {
    use std::process::Command;
    
    let output = if cfg!(target_os = "windows") {
        Command::new("ping").arg("-n").arg("1").arg(&host).output()
    } else {
        Command::new("ping").arg("-c").arg("1").arg(&host).output()
    };
    
    match output {
        Ok(out) => {
            let result = String::from_utf8_lossy(&out.stdout);
            Ok(result.to_string())
        }
        Err(e) => Err(e.to_string()),
    }
}

#[tauri::command]
fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

/// 截取全屏，返回 base64 编码的 PNG 图片数据 URI
#[tauri::command]
async fn capture_screenshot() -> Result<String, String> {
    use screenshots::Screen;

    let screens = Screen::all().map_err(|e| format!("获取屏幕失败: {}", e))?;
    let screen = screens.into_iter().next().ok_or("没有找到可用屏幕")?;

    let image = screen
        .capture()
        .map_err(|e| format!("截图失败: {}", e))?;

    let mut png_bytes: Vec<u8> = Vec::new();
    let mut cursor = std::io::Cursor::new(&mut png_bytes);
    image
        .write_to(&mut cursor, screenshots::image::ImageFormat::Png)
        .map_err(|e| format!("编码 PNG 失败: {}", e))?;
    let b64 = general_purpose::STANDARD.encode(&png_bytes);
    Ok(format!("data:image/png;base64,{}", b64))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            ping_host,
            get_app_version,
            capture_screenshot,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
