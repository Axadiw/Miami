import { calculateMarketValues } from '@/app/shared/components/positionCalculators/marketCalculator';

describe('calculateMarketValues', () => {
  it('should calculate longs in correct manner', () => {
    expect(
      calculateMarketValues({
        side: 'Long',
        openPrice: 100,
        accountBalance: 100,
        maxLoss: 10,
        maxLossType: '%',
        sl: 50,
        slType: '%',
        tp1: 100,
        tp1Type: '%',
        tp1Percent: 50,
        tp2: 200,
        tp2Type: '%',
        tp2Percent: 25,
        tp3: 300,
        tp3Type: '%',
        tp3Percent: 25,
      })
    ).toEqual({
      positionSize: 0.2,
      positionSizeUSD: 20,
      maxLossUSD: 10,
      maxLossPercent: 10,
      tp1USDReward: 10,
      tp1Price: 200,
      tp1Percent: 100,
      tp2USDReward: 20,
      tp2Price: 300,
      tp2Percent: 200,
      tp3USDReward: 35,
      tp3Price: 400,
      tp3Percent: 300,
      slPrice: 50,
      slPercent: 50,
    });
  });
  it('should calculate shorts in correct manner', () => {
    const sut = calculateMarketValues({
      side: 'Short',
      openPrice: 100,
      accountBalance: 100,
      maxLoss: 10,
      maxLossType: '%',
      sl: 50,
      slType: '%',
      tp1: 10,
      tp1Type: '%',
      tp1Percent: 50,
      tp2: 20,
      tp2Type: '%',
      tp2Percent: 25,
      tp3: 30,
      tp3Type: '%',
      tp3Percent: 25,
    });
    expect(sut.positionSize).toEqual(0.2);
    expect(sut.maxLossUSD).toEqual(10);
    expect(sut.maxLossPercent).toEqual(10);
    expect(sut.tp1USDReward).toBeCloseTo(1);
    expect(sut.tp1Price).toEqual(90);
    expect(sut.tp1Percent).toBeCloseTo(10);
    expect(sut.tp2USDReward).toBeCloseTo(2);
    expect(sut.tp2Price).toEqual(80);
    expect(sut.tp2Percent).toBeCloseTo(20);
    expect(sut.tp3USDReward).toBeCloseTo(3.5);
    expect(sut.tp3Price).toEqual(70);
    expect(sut.tp3Percent).toBeCloseTo(30);
    expect(sut.slPrice).toEqual(150);
    expect(sut.slPercent).toEqual(50);
  });
});
