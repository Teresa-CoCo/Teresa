// BMI Calculator
export function calculateBMI(weight: number, height: number): { bmi: number; level: string } {
  const bmi = weight / (height * height);
  let level: string;
  
  if (bmi < 18.5) {
    level = '偏瘦';
  } else if (bmi < 24) {
    level = '正常';
  } else if (bmi < 28) {
    level = '偏胖';
  } else {
    level = '肥胖';
  }
  
  return { bmi: Number(bmi.toFixed(2)), level };
}

// Electrical Calculator
export function calculateElectric(mode: number, values: number[]): number {
  // mode: 1=Ampere, 2=Voltage, 3=Ohm
  const [a, b] = values;
  
  switch (mode) {
    case 1: // Ampere: I = V / R
      return Number((b / a).toFixed(2));
    case 2: // Voltage: V = I * R
      return Number((a * b).toFixed(2));
    case 3: // Ohm: R = V / I
      return Number((b / a).toFixed(2));
    default:
      return 0;
  }
}

// Length Converter
export function convertLength(value: number, fromUnit: string): Record<string, number> {
  // Convert to meters first
  let meters: number;
  
  switch (fromUnit) {
    case '米':
      meters = value;
      break;
    case '英尺':
      meters = value * 0.3048;
      break;
    case '英寸':
      meters = value * 0.0254;
      break;
    case '英里':
      meters = value * 1609.34;
      break;
    case '码':
      meters = value * 0.9144;
      break;
    default:
      meters = value;
  }
  
  return {
    米: Number(meters.toFixed(4)),
    英尺: Number((meters * 3.2808).toFixed(4)),
    英寸: Number((meters * 39.3701).toFixed(4)),
    英里: Number((meters / 1609.34).toFixed(4)),
    码: Number((meters / 0.9144).toFixed(4)),
  };
}

// Binary/Decimal Converter
export function binaryToDecimal(binary: string): number {
  return parseInt(binary, 2);
}

export function decimalToBinary(decimal: number): string {
  return decimal.toString(2);
}

// Lucky Number Generator
export function generateLuckyNumber(): number {
  return Math.floor(Math.random() * 9) + 1;
}

export function generateLuck(): string {
  const levels = ['大吉', '中吉', '小吉', '吉', '半吉', '末吉', '凶', '半凶', '小凶', '大凶'];
  return levels[Math.floor(Math.random() * 10)];
}
