import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { CreateMarketPositionParams } from '@/api/createPositions/useCreateMarketPosition';
import { CreatePositionResponse } from '@/api/createPositions/positionsCreationTypes';

export type UseCreateScaledPositionResult = UseMutationResult<
  CreatePositionResponse,
  Error,
  CreateScaledPositionParams,
  unknown
>;

export interface CreateScaledPositionParams extends CreateMarketPositionParams {
  upperPrice: number;
  lowerPrice: number;
}

export const createScaledPosition = async (
  token: string | null | undefined,
  scaledParams: CreateScaledPositionParams
) => {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    return (await axios.request({
      method: 'post',
      url: `${BASE_URL}/exchange_create_scaled_position`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        account_id: scaledParams.accountId,
        side: scaledParams.side,
        symbol: scaledParams.symbol,
        position_size: scaledParams.positionSize,
        take_profits: scaledParams.takeProfits,
        stop_loss: scaledParams.stopLoss,
        soft_stop_loss_timeout: scaledParams.softStopLossTimeout,
        comment: scaledParams.comment,
        move_sl_to_breakeven_after_tp1: scaledParams.moveSlToBreakevenAfterTp1,
        helper_url: scaledParams.helperUrl,
        upper_price: scaledParams.upperPrice,
        lower_price: scaledParams.lowerPrice,
      }),
    })) as CreatePositionResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useCreateScaledPosition = (): UseCreateScaledPositionResult => {
  const { loginToken } = useLoginContext();
  return useMutation({
    mutationFn: (params: CreateScaledPositionParams) => createScaledPosition(loginToken, params),
  });
};
