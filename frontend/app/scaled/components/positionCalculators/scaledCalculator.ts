export type PriceTypeType = '%' | '$';
export type Side = 'Long' | 'Short';

export interface ScaledCalculatorProps {
  side: Side;
  upperPrice: number;
  lowerPrice: number;
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

export interface ScaledCalculatorResponse {
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

export const calculateScaledValues = (props: ScaledCalculatorProps): ScaledCalculatorResponse => {
  const isLong = props.side === 'Long';
  const upper = Number(props.upperPrice);
  const lower = Number(props.lowerPrice);
  const maxLoss = Number(props.maxLoss);
  const sl = Number(props.sl);
  const balance = Number(props.accountBalance);
  const tp1 = Number(props.tp1);
  const tp2 = Number(props.tp2);
  const tp3 = Number(props.tp3);
  const tp1CutPercent = Number(props.tp1Percent) / 100;
  const tp2CutPercent = Number(props.tp2Percent) / 100;
  const tp3CutPercent = Number(props.tp3Percent) / 100;

  const avgPrice = props.lowerPrice + (props.upperPrice - props.lowerPrice) / 2;

  const maxLossUSD = props.maxLossType === '$' ? maxLoss : (maxLoss / 100.0) * balance;

  const slStartLevel = isLong ? lower : upper;
  const slPrice = props.slType === '$' ? sl : slStartLevel * (1 + ((isLong ? -1 : 1) * sl) / 100.0);

  const slPercent = 100 * (isLong ? 1 - slPrice / slStartLevel : slPrice / slStartLevel - 1);
  const slPercentFromAvg = 100 * (isLong ? 1 - slPrice / avgPrice : slPrice / avgPrice - 1);
  const positionSize = maxLossUSD / ((avgPrice * slPercentFromAvg) / 100);
  const positionSizeUSD = positionSize * avgPrice;

  const tpStartLevel = isLong ? upper : lower;
  const tp1Price =
    props.tp1Type === '$' ? tp1 : tpStartLevel * (1 + ((isLong ? 1 : -1) * tp1) / 100.0);
  const tp1Percent = 100 * (isLong ? 1 : -1) * (tp1Price / tpStartLevel - 1);
  const tp2Price =
    props.tp2Type === '$' ? tp2 : tpStartLevel * (1 + ((isLong ? 1 : -1) * tp2) / 100.0);
  const tp2Percent = 100 * (isLong ? 1 : -1) * (tp2Price / tpStartLevel - 1);
  const tp3Price =
    props.tp3Type === '$' ? tp3 : tpStartLevel * (1 + ((isLong ? 1 : -1) * tp3) / 100.0);
  const tp3Percent = 100 * (isLong ? 1 : -1) * (tp3Price / tpStartLevel - 1);

  const tp1PercentFromAvg = 100 * (isLong ? 1 : -1) * (tp1Price / avgPrice - 1);
  const tp2PercentFromAvg = 100 * (isLong ? 1 : -1) * (tp2Price / avgPrice - 1);
  const tp3PercentFromAvg = 100 * (isLong ? 1 : -1) * (tp3Price / avgPrice - 1);

  const tp1USDReward = positionSize * avgPrice * (tp1PercentFromAvg / 100.0) * tp1CutPercent;
  const tp2USDReward =
    tp1USDReward + positionSize * avgPrice * (tp2PercentFromAvg / 100.0) * tp2CutPercent;
  const tp3USDReward =
    tp2USDReward + positionSize * avgPrice * (tp3PercentFromAvg / 100.0) * tp3CutPercent;
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
