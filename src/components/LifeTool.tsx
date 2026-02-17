import { useState } from 'react';
import { Calculator, Zap, Leaf, Network, Ruler, Binary, Gem } from 'lucide-react';
import { 
  calculateBMI, 
  calculateElectric, 
  convertLength, 
  binaryToDecimal, 
  decimalToBinary,
  generateLuckyNumber,
  generateLuck 
} from '../utils/tools';

type Tool = 'bmi' | 'electric' | 'lucky' | 'ping' | 'length' | 'binary';

const tools = [
  { id: 'bmi', name: 'BMI计算', icon: Calculator },
  { id: 'electric', name: '万能表', icon: Zap },
  { id: 'lucky', name: '幸运与运势', icon: Gem },
  { id: 'ping', name: 'Ping网络', icon: Network },
  { id: 'length', name: '长度转换', icon: Ruler },
  { id: 'binary', name: '十进制/二进制', icon: Binary },
];

export function LifeTool() {
  const [activeTool, setActiveTool] = useState<Tool | null>(null);
  const [result, setResult] = useState<string>('');

  // BMI State
  const [bmiWeight, setBmiWeight] = useState('');
  const [bmiHeight, setBmiHeight] = useState('');

  // Electric State
  const [electricMode, setElectricMode] = useState(1);
  const [electricA, setElectricA] = useState('');
  const [electricB, setElectricB] = useState('');

  // Length State
  const [lengthValue, setLengthValue] = useState('');
  const [lengthUnit, setLengthUnit] = useState('米');

  // Binary State
  const [binaryInput, setBinaryInput] = useState('');

  const handleBMI = () => {
    const w = parseFloat(bmiWeight);
    const h = parseFloat(bmiHeight);
    if (!w || !h) {
      setResult('请输入有效的体重和身高');
      return;
    }
    const { bmi, level } = calculateBMI(w, h);
    setResult(`BMI: ${bmi}\n等级: ${level}`);
  };

  const handleElectric = () => {
    const a = parseFloat(electricA);
    const b = parseFloat(electricB);
    if (!a || !b) {
      setResult('请输入有效的数值');
      return;
    }
    const r = calculateElectric(electricMode, [a, b]);
    const modeName = ['安培', '电压', '欧姆'][electricMode - 1];
    setResult(`${modeName}: ${r}`);
  };

  const handleLength = () => {
    const v = parseFloat(lengthValue);
    if (!v) {
      setResult('请输入有效的数值');
      return;
    }
    const r = convertLength(v, lengthUnit);
    setResult(
      Object.entries(r)
        .map(([k, val]) => `${k}: ${val}`)
        .join('\n')
    );
  };

  const handleBinaryToDecimal = () => {
    if (!/^[01]+$/.test(binaryInput)) {
      setResult('请输入有效的二进制数');
      return;
    }
    const r = binaryToDecimal(binaryInput);
    setResult(`十进制: ${r}`);
  };

  const handleDecimalToBinary = () => {
    const v = parseInt(binaryInput);
    if (isNaN(v)) {
      setResult('请输入有效的十进制数');
      return;
    }
    const r = decimalToBinary(v);
    setResult(`二进制: ${r}`);
  };

  const handleLucky = () => {
    const num = generateLuckyNumber();
    const luck = generateLuck();
    setResult(`幸运数字: ${num}\n今日运势: ${luck}`);
  };

  const renderTool = () => {
    switch (activeTool) {
      case 'bmi':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">BMI 计算器</h3>
            <div>
              <label className="block text-sm mb-1">体重 (kg)</label>
              <input
                type="number"
                value={bmiWeight}
                onChange={(e) => setBmiWeight(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
                placeholder="例如: 70"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">身高 (m)</label>
              <input
                type="number"
                value={bmiHeight}
                onChange={(e) => setBmiHeight(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
                placeholder="例如: 1.75"
              />
            </div>
            <button onClick={handleBMI} className="px-4 py-2 bg-blue-500 text-white rounded-lg">
              计算
            </button>
          </div>
        );

      case 'electric':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">万能表</h3>
            <div className="flex gap-2">
              {[1, 2, 3].map((m) => (
                <button
                  key={m}
                  onClick={() => setElectricMode(m)}
                  className={`px-3 py-1 rounded ${electricMode === m ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}
                >
                  {['安培', '电压', '欧姆'][m - 1]}
                </button>
              ))}
            </div>
            <div>
              <label className="block text-sm mb-1">数值 A</label>
              <input
                type="number"
                value={electricA}
                onChange={(e) => setElectricA(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">数值 B</label>
              <input
                type="number"
                value={electricB}
                onChange={(e) => setElectricB(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
              />
            </div>
            <button onClick={handleElectric} className="px-4 py-2 bg-blue-500 text-white rounded-lg">
              计算
            </button>
          </div>
        );

      case 'lucky':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">幸运数与运势</h3>
            <button onClick={handleLucky} className="px-4 py-2 bg-purple-500 text-white rounded-lg">
              生成幸运
            </button>
          </div>
        );

      case 'ping':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">Ping 网络工具</h3>
            <p className="text-gray-500">点击按钮测试网络连接</p>
            <div className="flex gap-2">
              <button 
                onClick={() => setResult('测试 google.com...')}
                className="px-3 py-2 bg-green-500 text-white rounded-lg"
              >
                Ping 国外
              </button>
              <button 
                onClick={() => setResult('测试 baidu.com...')}
                className="px-3 py-2 bg-green-500 text-white rounded-lg"
              >
                Ping 国内
              </button>
            </div>
            <p className="text-xs text-gray-500">注: 实际 Ping 功能需要后端支持</p>
          </div>
        );

      case 'length':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">长度转换</h3>
            <div>
              <label className="block text-sm mb-1">输入单位</label>
              <select
                value={lengthUnit}
                onChange={(e) => setLengthUnit(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
              >
                {['米', '英尺', '英寸', '英里', '码'].map((u) => (
                  <option key={u} value={u}>{u}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">数值</label>
              <input
                type="number"
                value={lengthValue}
                onChange={(e) => setLengthValue(e.target.value)}
                className="w-full rounded-lg border p-2 dark:bg-gray-800"
              />
            </div>
            <button onClick={handleLength} className="px-4 py-2 bg-blue-500 text-white rounded-lg">
              转换
            </button>
          </div>
        );

      case 'binary':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-bold">十进制/二进制转换</h3>
            <input
              type="text"
              value={binaryInput}
              onChange={(e) => setBinaryInput(e.target.value)}
              className="w-full rounded-lg border p-2 dark:bg-gray-800"
              placeholder="输入数字"
            />
            <div className="flex gap-2">
              <button onClick={handleBinaryToDecimal} className="px-3 py-2 bg-blue-500 text-white rounded-lg">
                二→十
              </button>
              <button onClick={handleDecimalToBinary} className="px-3 py-2 bg-blue-500 text-white rounded-lg">
                十→二
              </button>
            </div>
          </div>
        );

      default:
        return (
          <div className="grid grid-cols-2 gap-4">
            {tools.map((t) => {
              const Icon = t.icon;
              return (
                <button
                  key={t.id}
                  onClick={() => setActiveTool(t.id as Tool)}
                  className="flex flex-col items-center gap-2 p-4 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <Icon size={32} />
                  <span>{t.name}</span>
                </button>
              );
            })}
          </div>
        );
    }
  };

  return (
    <div className="p-4 h-full flex flex-col">
      <h2 className="text-2xl font-bold mb-4">🧰 生活工具箱</h2>
      
      <div className="flex-1 overflow-auto">
        {renderTool()}
      </div>

      {result && (
        <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <pre className="whitespace-pre-wrap">{result}</pre>
          {activeTool && (
            <button
              onClick={() => setActiveTool(null)}
              className="mt-2 text-sm text-blue-500"
            >
              ← 返回工具列表
            </button>
          )}
        </div>
      )}
    </div>
  );
}
