import { calculateScaledValues } from '@/app/scaled/components/positionCalculators/scaledCalculator';

describe('calculateScaledValues', () => {
  it('should calculate longs in correct manner', () => {
    expect(
      calculateScaledValues({
        side: 'Long',
        upperPrice: 150,
        lowerPrice: 50,
        accountBalance: 100,
        maxLoss: 10,
        maxLossType: '%',
        sl: 40,
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
      positionSize: 0.14285714285714285,
      positionSizeUSD: 14.285714285714285,
      maxLossUSD: 10,
      maxLossPercent: 10,
      tp1USDReward: 14.285714285714285,
      tp1Price: 300,
      tp1Percent: 100,
      tp2USDReward: 26.785714285714285,
      tp2Price: 450,
      tp2Percent: 200,
      tp3USDReward: 44.64285714285714,
      tp3Price: 600,
      tp3Percent: 300,
      slPrice: 30,
      slPercent: 40,
    });
  });
  it('should calculate shorts in correct manner', () => {
    const sut = calculateScaledValues({
      side: 'Short',
      upperPrice: 150,
      lowerPrice: 50,
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
    expect(sut.positionSize).toEqual(0.08);
    expect(sut.maxLossUSD).toEqual(10);
    expect(sut.maxLossPercent).toEqual(10);
    expect(sut.tp1USDReward).toBeCloseTo(2.2);
    expect(sut.tp1Price).toEqual(45);
    expect(sut.tp1Percent).toBeCloseTo(10);
    expect(sut.tp2USDReward).toBeCloseTo(3.4);
    expect(sut.tp2Price).toEqual(40);
    expect(sut.tp2Percent).toBeCloseTo(19.9999);
    expect(sut.tp3USDReward).toBeCloseTo(4.7);
    expect(sut.tp3Price).toEqual(35);
    expect(sut.tp3Percent).toBeCloseTo(30);
    expect(sut.slPrice).toEqual(225);
    expect(sut.slPercent).toEqual(50);
  });
});
