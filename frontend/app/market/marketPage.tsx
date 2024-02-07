'use client';

import {
  Button,
  Group,
  NumberFormatter,
  NumberInput,
  SegmentedControl,
  Select,
  Space,
  Switch,
  Text,
  useMantineColorScheme,
} from '@mantine/core';
import { useEffect, useState } from 'react';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import { ChartComponent } from '@/app/account/components/chart/chart';
import {
  calculateMarketValues,
  PriceTypeType,
  Side,
} from '@/app/account/components/positionCalculators/marketCalculator';

export default function MarketPage() {
  const exchange = 'bybit';
  const limit = 1000;
  const { colorScheme } = useMantineColorScheme();
  const isDarkTheme = colorScheme === 'dark';
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [accountBalance, setAccountBalance] = useState<number>(500);
  const [maxLoss, setMaxLoss] = useState<number | string | undefined>(undefined);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [selectedTimeframe, setSelectedTimeframe] = useState<string | null>(null);
  const [sl, setSl] = useState<number | string | undefined>(undefined);
  const [maxLossType, setMaxLossType] = useState<PriceTypeType>('%');
  const [slType, setSlType] = useState<PriceTypeType>('%');
  const [tp1Type, setTp1Type] = useState<PriceTypeType>('%');
  const [tp2Type, setTp2Type] = useState<PriceTypeType>('%');
  const [tp3Type, setTp3Type] = useState<PriceTypeType>('%');
  const [tp1, setTp1] = useState<number | string | undefined>(undefined);
  const [tp2, setTp2] = useState<number | string | undefined>(undefined);
  const [tp3, setTp3] = useState<number | string | undefined>(undefined);
  const [tp1Percent, setTp1Percent] = useState<number | string | undefined>(undefined);
  const [tp2Percent, setTp2Percent] = useState<number | string | undefined>(undefined);
  const [tp3Percent, setTp3Percent] = useState<number | string | undefined>(undefined);
  const [slToBreakEvenAtTp1, setSlToBreakEvenAtTp1] = useState(false);

  const [side, setSide] = useState<Side>('Buy');

  const dataLayer = useDataLayerContext();
  const { data: timeframes } = dataLayer.useGetTimeframes({ exchange });

  const calculateAmountColor = (value: number) =>
    value === 0 ? (isDarkTheme ? 'white' : 'black') : value > 0 ? 'green' : 'red';

  const calculateAmountSign = (value: number) => (value === 0 ? '' : value > 0 ? '+' : '');

  const { data: ohlcvs } = dataLayer.useGetOHLCVs({
    exchange,
    symbol: selectedSymbol ?? '',
    timeframe: selectedTimeframe ?? '',
    limit,
  });

  useEffect(() => {
    if (timeframes && timeframes.timeframes.length > 0) {
      setSelectedTimeframe(timeframes.timeframes.includes('1h') ? '1h' : timeframes.timeframes[0]);
    }
  }, [timeframes]);

  const { isSuccess: fetchSymbolsSuccess, data: symbols } = dataLayer.useGetSymbols({ exchange });

  const currentPrice = ohlcvs?.ohlcvs.at(-1)?.close ?? 0;
  const calculatedValues = calculateMarketValues({
    side,
    openPrice: currentPrice,
    accountBalance,
    maxLoss,
    maxLossType,
    sl,
    tp1,
    tp2,
    tp3,
    tp1Percent,
    tp2Percent,
    tp3Percent,
    slType,
    tp1Type,
    tp2Type,
    tp3Type,
  });
  return (
    <>
      <Group>
        <Text>Balance:</Text>
        <NumberFormatter prefix="$ " value={`${accountBalance}`} thousandSeparator />
      </Group>
      {fetchSymbolsSuccess && (
        <Select
          label="Symbol"
          placeholder="Pick symbol"
          data={symbols.symbols}
          value={selectedSymbol}
          onChange={setSelectedSymbol}
          searchable
        />
      )}
      <Text>Current price: {currentPrice}</Text>
      <Group>
        <Text>Side:</Text>
        <SegmentedControl
          onChange={(v) => setSide(v as Side)}
          value={side}
          color={side === 'Buy' ? 'green' : 'red'}
          data={['Buy', 'Sell']}
        />
      </Group>
      <Text>Position size: {calculatedValues.positionSize.toFixed(6)}</Text>
      <Group>
        <Text>Max loss:</Text>
        <NumberInput size="xs" value={maxLoss} onChange={setMaxLoss} />
        <SegmentedControl
          value={maxLossType}
          onChange={(v) => setMaxLossType(v as PriceTypeType)}
          data={['%', '$']}
        />
        <Text>
          {`$${calculatedValues.maxLossUSD.toFixed(2)} (${calculatedValues.maxLossPercent.toFixed(
            2
          )}%)`}
        </Text>
      </Group>

      <Text size="xs" c="green">
        Take profit 1:
      </Text>
      <Group>
        <Text>Price</Text>
        <NumberInput size="xs" value={tp1} onChange={setTp1} />
        <SegmentedControl
          value={tp1Type}
          onChange={(v) => setTp1Type(v as PriceTypeType)}
          data={['%', '$']}
        />
        <Text c={calculateAmountColor(calculatedValues.tp1Percent)}>
          {`$${calculatedValues.tp1Price.toFixed(2)} (${calculatedValues.tp1Percent.toFixed(2)}%)`}
        </Text>
        <Text>Percent</Text>
        <NumberInput size="xs" value={tp1Percent} onChange={setTp1Percent} />
        <Text c={calculateAmountColor(calculatedValues.tp1USDReward)}>
          {`$ ${calculateAmountSign(
            calculatedValues.tp1USDReward
          )}${calculatedValues.tp1USDReward.toFixed(2)}`}
        </Text>
      </Group>
      <Text size="xs" c="green">
        Take profit 2:
      </Text>
      <Group>
        <Text>Price</Text>
        <NumberInput size="xs" value={tp2} onChange={setTp2} />
        <SegmentedControl
          value={tp2Type}
          onChange={(v) => setTp2Type(v as PriceTypeType)}
          data={['%', '$']}
        />
        <Text c={calculateAmountColor(calculatedValues.tp2Percent)}>
          {`$${calculatedValues.tp2Price.toFixed(2)} (${calculatedValues.tp2Percent.toFixed(2)}%)`}
        </Text>
        <Text>Percent</Text>
        <NumberInput size="xs" value={tp2Percent} onChange={setTp2Percent} />
        <Text c={calculateAmountColor(calculatedValues.tp2USDReward)}>
          {`$ ${calculateAmountSign(
            calculatedValues.tp2USDReward
          )}${calculatedValues.tp2USDReward.toFixed(2)}`}
        </Text>
      </Group>
      <Text size="xs" c="green">
        Take profit 3:
      </Text>
      <Group>
        <Text>Price</Text>
        <NumberInput size="xs" value={tp3} onChange={setTp3} />
        <SegmentedControl
          value={tp3Type}
          onChange={(v) => setTp3Type(v as PriceTypeType)}
          data={['%', '$']}
        />
        <Text c={calculateAmountColor(calculatedValues.tp3Percent)}>
          {`$${calculatedValues.tp3Price.toFixed(2)} (${calculatedValues.tp3Percent.toFixed(2)}%)`}
        </Text>
        <Text>Percent</Text>
        <NumberInput size="xs" value={tp3Percent} onChange={setTp3Percent} />
        <Text c={calculateAmountColor(calculatedValues.tp3USDReward)}>
          {`$ ${calculateAmountSign(
            calculatedValues.tp3USDReward
          )}${calculatedValues.tp3USDReward.toFixed(2)}`}
        </Text>
      </Group>
      <Text size="xs" c="red">
        Stop loss
      </Text>
      <Group>
        <Text>Price</Text>
        <NumberInput size="xs" value={sl} onChange={setSl} />
        <SegmentedControl
          value={slType}
          onChange={(v) => setSlType(v as PriceTypeType)}
          data={['%', '$']}
        />
        <Text c="red">
          {`$${calculatedValues.slPrice.toFixed(2)} (${calculatedValues.slPercent.toFixed(2)}%)`}
        </Text>
      </Group>
      <Switch
        label="Move SL to breakeven at TP1"
        checked={slToBreakEvenAtTp1}
        onChange={(event) => setSlToBreakEvenAtTp1(event.currentTarget.checked)}
      />
      <Space h="md" />
      <ChartComponent
        isDarkTheme={isDarkTheme}
        data={ohlcvs?.ohlcvs ?? []}
        tp1Price={Number(tp1)}
        tp2Price={Number(tp2)}
        tp3Price={Number(tp3)}
        sl={Number(sl)}
      />
      <Group>
        {timeframes &&
          timeframes.timeframes.map((timeframe) => (
            <Button
              key={`tf-${timeframe}`}
              variant={timeframe === selectedTimeframe ? 'filled' : 'default'}
              size="xs"
              onClick={() => setSelectedTimeframe(timeframe)}
            >
              {timeframe}
            </Button>
          ))}
      </Group>
      <Space h="md" />
      <Button>Execute</Button>
      <Space h="md" />
      <Text />
    </>
  );
}
