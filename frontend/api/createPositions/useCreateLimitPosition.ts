import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import { CreateMarketPositionParams } from '@/api/createPositions/useCreateMarketPosition';
import { CreatePositionResponse } from '@/api/createPositions/positionsCreationTypes';

export type UseCreateLimitPositionResult = UseMutationResult<
  CreatePositionResponse,
  Error,
  CreateLimitPositionParams,
  unknown
>;

export interface CreateLimitPositionParams extends CreateMarketPositionParams {
  limitPrice: number;
}

export const createLimitPosition = async (
  token: string | null | undefined,
  limitParams: CreateLimitPositionParams
) => {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    return (await axios.request({
      method: 'post',
      url: `${BASE_URL}/exchange_create_limit_position`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        account_id: limitParams.accountId,
        side: limitParams.side,
        symbol: limitParams.symbol,
        position_size: limitParams.positionSize,
        take_profits: limitParams.takeProfits,
        stop_loss: limitParams.stopLoss,
        soft_stop_loss_timeout: limitParams.softStopLossTimeout,
        comment: limitParams.comment,
        move_sl_to_breakeven_after_tp1: limitParams.moveSlToBreakevenAfterTp1,
        helper_url: limitParams.helperUrl,
        limit_price: limitParams.limitPrice,
      }),
    })) as CreatePositionResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useCreateLimitPosition = (): UseCreateLimitPositionResult => {
  const { loginToken } = useLoginContext();
  return useMutation({
    mutationFn: (params: CreateLimitPositionParams) => createLimitPosition(loginToken, params),
  });
};
