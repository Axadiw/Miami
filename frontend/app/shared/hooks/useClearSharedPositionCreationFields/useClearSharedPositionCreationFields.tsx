import { useSharedPositionContext } from '@/contexts/SharedPositionContext/SharedPositionContext';

export const useClearSharedPositionCreationFields = () => {
  const {
    setSl,
    setTp1,
    setTp2,
    setTp3,
    setTp1Type,
    setTp2Type,
    setTp3Type,
    setSlType,
    setMaxLossType,
    setExternalChartHelperURL,
    setSelectedSymbol,
    setMaxLoss,
  } = useSharedPositionContext();

  return () => {
    setSelectedSymbol(null);
    setMaxLoss('');
    setSl('');
    setTp1('');
    setTp2('');
    setTp3('');
    setTp1Type('%');
    setTp2Type('%');
    setTp3Type('%');
    setSlType('%');
    setMaxLossType('%');
    setExternalChartHelperURL('');
  };
};
