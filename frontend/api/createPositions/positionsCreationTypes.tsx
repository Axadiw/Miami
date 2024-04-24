import { Side } from '@/app/market/components/positionCalculators/marketCalculator';

export interface CreatePositionResponse {
  message: string;
  error?: string;
}

export interface CreatePositionParams {
  accountId: number;
  side: Side;
  symbol: string;
  positionSize: number;
  takeProfits: number[][];
  stopLoss: number;
  softStopLossTimeout: number;
  comment: string;
  moveSlToBreakevenAfterTp1: boolean;
  helperUrl: string;
}
