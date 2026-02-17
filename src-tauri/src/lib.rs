use serde::{Deserialize, Serialize};

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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            ping_host,
            get_app_version
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
