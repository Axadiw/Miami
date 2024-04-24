export type PriceTypeType = '%' | '$';
export type Side = 'Long' | 'Short';

export interface MarketCalculatorProps {
  side: Side;
  openPrice: number;
  accountBalance: number;
  maxLoss: number | string | undefined;
  maxLossType: PriceTypeType;
  sl: number | string | undefined;
  tp1: number | string | undefined;
  tp2: number | string | undefined;
  tp3: number | string | undefined;
  tp1Percent: number | string | undefined;
  tp2Percent: number | string | undefined;
  tp3Percent: number | string | undefined;
  slType: PriceTypeType;
  tp1Type: PriceTypeType;
  tp2Type: PriceTypeType;
  tp3Type: PriceTypeType;
}

export interface MarketCalculatorResponse {
  positionSize: number;
  positionSizeUSD: number;
  maxLossUSD: number;
  maxLossPercent: number;
  tp1USDReward: number;
  tp1Price: number;
  tp1Percent: number;
  tp2USDReward: number;
  tp2Price: number;
  tp2Percent: number;
  tp3USDReward: number;
  tp3Price: number;
  tp3Percent: number;
  slPrice: number;
  slPercent: number;
}

export const calculateMarketValues = (props: MarketCalculatorProps): MarketCalculatorResponse => {
  const isLong = props.side === 'Long';
  const maxLoss = Number(props.maxLoss);
  const sl = Number(props.sl);
  const balance = Number(props.accountBalance);
  const tp1 = Number(props.tp1);
  const tp2 = Number(props.tp2);
  const tp3 = Number(props.tp3);
  const tp1CutPercent = Number(props.tp1Percent) / 100;
  const tp2CutPercent = Number(props.tp2Percent) / 100;
  const tp3CutPercent = Number(props.tp3Percent) / 100;

  const maxLossUSD = props.maxLossType === '$' ? maxLoss : (maxLoss / 100.0) * balance;

  const slPrice =
    props.slType === '$' ? sl : props.openPrice * (1 + ((isLong ? -1 : 1) * sl) / 100.0);

  const slPercent = 100 * (isLong ? 1 - slPrice / props.openPrice : slPrice / props.openPrice - 1);
  const positionSize = maxLossUSD / ((props.openPrice * slPercent) / 100);
  const positionSizeUSD = positionSize * props.openPrice;
  const tp1Price =
    props.tp1Type === '$' ? tp1 : props.openPrice * (1 + ((isLong ? 1 : -1) * tp1) / 100.0);
  const tp1Percent = 100 * (isLong ? 1 : -1) * (tp1Price / props.openPrice - 1);
  const tp2Price =
    props.tp2Type === '$' ? tp2 : props.openPrice * (1 + ((isLong ? 1 : -1) * tp2) / 100.0);
  const tp2Percent = 100 * (isLong ? 1 : -1) * (tp2Price / props.openPrice - 1);
  const tp3Price =
    props.tp3Type === '$' ? tp3 : props.openPrice * (1 + ((isLong ? 1 : -1) * tp3) / 100.0);
  const tp3Percent = 100 * (isLong ? 1 : -1) * (tp3Price / props.openPrice - 1);

  const tp1USDReward = positionSize * props.openPrice * (tp1Percent / 100.0) * tp1CutPercent;
  const tp2USDReward =
    tp1USDReward + positionSize * props.openPrice * (tp2Percent / 100.0) * tp2CutPercent;
  const tp3USDReward =
    tp2USDReward + positionSize * props.openPrice * (tp3Percent / 100.0) * tp3CutPercent;
  return {
    positionSize,
    positionSizeUSD,
    maxLossUSD,
    maxLossPercent: (maxLossUSD / balance) * 100.0,
    tp1USDReward,
    tp1Price,
    tp1Percent,
    tp2USDReward,
    tp2Price,
    tp2Percent,
    tp3USDReward,
    tp3Price,
    tp3Percent,
    slPrice,
    slPercent,
  };
};
