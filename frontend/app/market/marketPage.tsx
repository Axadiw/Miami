'use client';

import {
  Button,
  Group,
  Input,
  NumberFormatter,
  NumberInput,
  rem,
  SegmentedControl,
  Space,
  Stack,
  Switch,
  Text,
  TextInput,
  Timeline,
  useMantineColorScheme,
} from '@mantine/core';
import { useEffect, useState } from 'react';
import { Spotlight, spotlight } from '@mantine/spotlight';
import {
  IconNumber0,
  IconNumber1,
  IconNumber2,
  IconNumber3,
  IconNumber4,
  IconSearch,
} from '@tabler/icons-react';
import { useDataLayerContext } from '@/contexts/DataLayerContext/DataLayerContext';
import {
  calculateMarketValues,
  PriceTypeType,
  Side,
} from '@/app/account/components/positionCalculators/marketCalculator';
import { ChartComponent } from '@/app/account/components/chart/chart';

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
  const [iframeURL, setIFrameURL] = useState<string | undefined>(undefined);

  const [side, setSide] = useState<Side>('Buy');

  const dataLayer = useDataLayerContext();
  const { data: timeframes } = dataLayer.useGetTimeframes({ exchange });

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

  const currentPrice = ohlcvs?.ohlcvs.at(-1)?.close ?? -1;
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

  const step1Finished = selectedSymbol !== null;
  const step2Finished = maxLoss !== undefined && sl !== undefined;
  const step3Finished =
    tp1 !== undefined &&
    tp1Percent !== undefined &&
    tp2 !== undefined &&
    tp2Percent !== undefined &&
    tp3 !== undefined &&
    tp3Percent !== undefined;

  let active = 1;
  if (step1Finished) {
    active = 2;
  }
  if (step1Finished && step2Finished) {
    active = 3;
  }
  if (step1Finished && step2Finished && step3Finished) {
    active = 4;
  }

  return (
    <Stack>
      <Group grow align="flex-start">
        <Stack>
          <Group>
            <Text>Balance:</Text>
            <NumberFormatter prefix="$ " value={`${accountBalance}`} thousandSeparator />
          </Group>
          <Text>Position size: {calculatedValues.positionSize.toFixed(6)}</Text>
          <Timeline active={active} bulletSize={24} lineWidth={2}>
            <Timeline.Item bullet={<IconNumber0 size={20} />}>
              <Group>
                <SegmentedControl
                  onChange={(v) => setSide(v as Side)}
                  value={side}
                  color={side === 'Buy' ? 'green' : 'red'}
                  data={['Buy', 'Sell']}
                />
              </Group>
            </Timeline.Item>
            <Timeline.Item bullet={<IconNumber1 size={20} />}>
              {fetchSymbolsSuccess && (
                <>
                  <Group>
                    <Button size="xs" onClick={spotlight.open}>
                      Pick symbol
                    </Button>
                    <Spotlight
                      actions={symbols?.symbols.map((value, index) => ({
                        id: `symbol-${index}`,
                        label: `${value}\n`,
                        onClick: () => setSelectedSymbol(value),
                      }))}
                      nothingFound="Nothing found..."
                      highlightQuery
                      scrollable
                      searchProps={{
                        leftSection: (
                          <IconSearch style={{ width: rem(20), height: rem(20) }} stroke={1.5} />
                        ),
                        placeholder: 'Select symbol...',
                      }}
                    />
                  </Group>
                </>
              )}
              {selectedSymbol && <Text>Selected {selectedSymbol}</Text>}
              {currentPrice >= 0 && <Text>Current price: $ {currentPrice}</Text>}
            </Timeline.Item>
            <Timeline.Item bullet={<IconNumber2 size={20} />}>
              <Input.Wrapper label="Max loss:" size="xs">
                <Group>
                  <NumberInput
                    disabled={active < 2}
                    w="100px"
                    size="xs"
                    value={maxLoss}
                    onChange={setMaxLoss}
                  />
                  <SegmentedControl
                    value={maxLossType}
                    disabled={active < 2}
                    onChange={(v) => setMaxLossType(v as PriceTypeType)}
                    color={maxLossType === '%' ? 'yellow' : 'violet'}
                    data={['%', '$']}
                  />
                  <Text>
                    {maxLoss && maxLossType === '%' && `$${calculatedValues.maxLossUSD.toFixed(2)}`}
                    {maxLoss &&
                      maxLossType === '$' &&
                      `(${calculatedValues.maxLossPercent.toFixed(2)}%)`}
                  </Text>
                </Group>
              </Input.Wrapper>
              <Input.Wrapper label="Stop loss" size="xs">
                <Group>
                  <Text>Price</Text>
                  <NumberInput
                    disabled={active < 2}
                    w="100px"
                    size="xs"
                    value={sl}
                    onChange={setSl}
                  />
                  <SegmentedControl
                    disabled={active < 2}
                    value={slType}
                    color={slType === '%' ? 'yellow' : 'violet'}
                    onChange={(v) => setSlType(v as PriceTypeType)}
                    data={['%', '$']}
                  />
                  <Text>
                    {sl && slType === '%' && `$${calculatedValues.slPrice.toFixed(6)}`}
                    {sl && slType === '$' && `${calculatedValues.slPercent.toFixed(2)}%`}
                  </Text>
                </Group>
              </Input.Wrapper>
            </Timeline.Item>
            <Timeline.Item bullet={<IconNumber3 size={20} />}>
              <Input.Wrapper label="Take profit 1:" size="xs">
                <Group>
                  <Text>Price</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="100px"
                    size="xs"
                    value={tp1}
                    onChange={setTp1}
                  />
                  <SegmentedControl
                    disabled={active < 3}
                    value={tp1Type}
                    onChange={(v) => setTp1Type(v as PriceTypeType)}
                    color={tp1Type === '%' ? 'yellow' : 'violet'}
                    data={['%', '$']}
                  />
                  <Text>
                    {tp1 && tp1Type === '%' && `$${calculatedValues.tp1Price.toFixed(2)}`}
                    {tp1 && tp1Type === '$' && `(${calculatedValues.tp1Percent.toFixed(2)}%)`}
                  </Text>
                  <Text>Volume</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="50px"
                    size="xs"
                    value={tp1Percent}
                    onChange={setTp1Percent}
                  />
                  <Text c="green">
                    {tp1 &&
                      tp1Percent &&
                      `$ ${calculateAmountSign(
                        calculatedValues.tp1USDReward
                      )}${calculatedValues.tp1USDReward.toFixed(2)}`}
                  </Text>
                </Group>
              </Input.Wrapper>
              <Input.Wrapper label="Take profit 2:" size="xs">
                <Group>
                  <Text>Price</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="100px"
                    size="xs"
                    value={tp2}
                    onChange={setTp2}
                  />
                  <SegmentedControl
                    disabled={active < 3}
                    value={tp2Type}
                    color={tp2Type === '%' ? 'yellow' : 'violet'}
                    onChange={(v) => setTp2Type(v as PriceTypeType)}
                    data={['%', '$']}
                  />
                  <Text>
                    {tp2 && tp2Type === '%' && `$${calculatedValues.tp2Price.toFixed(2)}`}
                    {tp2 && tp2Type === '$' && `(${calculatedValues.tp2Percent.toFixed(2)}%)`}
                  </Text>
                  <Text>Volume</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="50px"
                    size="xs"
                    value={tp2Percent}
                    onChange={setTp2Percent}
                  />
                  <Text c="green">
                    {tp2 &&
                      tp2Percent &&
                      `$ ${calculateAmountSign(
                        calculatedValues.tp2USDReward
                      )}${calculatedValues.tp2USDReward.toFixed(2)}`}
                  </Text>
                </Group>
              </Input.Wrapper>
              <Input.Wrapper label="Take profit 3:" size="xs">
                <Group>
                  <Text>Price</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="100px"
                    size="xs"
                    value={tp3}
                    onChange={setTp3}
                  />
                  <SegmentedControl
                    disabled={active < 3}
                    value={tp3Type}
                    color={tp3Type === '%' ? 'yellow' : 'violet'}
                    onChange={(v) => setTp3Type(v as PriceTypeType)}
                    data={['%', '$']}
                  />
                  <Text>
                    {tp3 && tp3Type === '%' && `$${calculatedValues.tp3Price.toFixed(2)}`}
                    {tp3 && tp3Type === '$' && `(${calculatedValues.tp3Percent.toFixed(2)}%)`}
                  </Text>
                  <Text>Volume</Text>
                  <NumberInput
                    disabled={active < 3}
                    w="50px"
                    size="xs"
                    value={tp3Percent}
                    onChange={setTp3Percent}
                  />
                  <Text c="green">
                    {tp3 &&
                      tp3Percent &&
                      `$ ${calculateAmountSign(
                        calculatedValues.tp3USDReward
                      )}${calculatedValues.tp3USDReward.toFixed(2)}`}
                  </Text>
                </Group>
              </Input.Wrapper>
            </Timeline.Item>
            <Timeline.Item bullet={<IconNumber4 size={20} />}>
              <Switch
                disabled={active < 4}
                label="Move SL to breakeven at TP1"
                checked={slToBreakEvenAtTp1}
                onChange={(event) => setSlToBreakEvenAtTp1(event.currentTarget.checked)}
              />
            </Timeline.Item>
          </Timeline>
          <Space h="md" />
        </Stack>

        <Stack>
          <Stack>
            <ChartComponent
              isDarkTheme={isDarkTheme}
              data={ohlcvs?.ohlcvs ?? []}
              tp1Price={Number(calculatedValues.tp1Price)}
              tp2Price={Number(calculatedValues.tp2Price)}
              tp3Price={Number(calculatedValues.tp3Price)}
              sl={Number(calculatedValues.slPrice)}
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
            {iframeURL && <img alt="Helper" src={iframeURL} height={300} />}
            <TextInput
              size="xs"
              value={iframeURL}
              onChange={(v) => setIFrameURL(v.currentTarget.value)}
              label="URL"
              placeholder="type URL"
            />
          </Stack>
          <Space h="md" />
          <Button disabled={active < 4}>Execute</Button>
        </Stack>
      </Group>
    </Stack>
  );
}
