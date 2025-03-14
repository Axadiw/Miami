import axios from 'axios';
import { useMutation, UseMutationResult } from '@tanstack/react-query';
import { BASE_URL } from '@/app/consts';
import { useLoginContext } from '@/contexts/LoginContext/LoginContext';
import {
  CreatePositionParams,
  CreatePositionResponse,
} from '@/api/createPositions/positionsCreationTypes';

export type UseCreateMarketPositionResult = UseMutationResult<
  CreatePositionResponse,
  Error,
  CreateMarketPositionParams,
  unknown
>;

export interface CreateMarketPositionParams extends CreatePositionParams {}

export const createMarketPosition = async (
  token: string | null | undefined,
  marketParams: CreateMarketPositionParams
) => {
  if (!token) {
    return Promise.reject(NotLoggedInError);
  }

  try {
    return (await axios.request({
      method: 'post',
      url: `${BASE_URL}/exchange_create_market_position`,
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': token,
      },
      data: JSON.stringify({
        account_id: marketParams.accountId,
        side: marketParams.side,
        symbol: marketParams.symbol,
        position_size: marketParams.positionSize,
        take_profits: marketParams.takeProfits,
        stop_loss: marketParams.stopLoss,
        soft_stop_loss_timeout: marketParams.softStopLossTimeout,
        comment: marketParams.comment,
        move_sl_to_breakeven_after_tp1: marketParams.moveSlToBreakevenAfterTp1,
        helper_url: marketParams.helperUrl,
      }),
    })) as CreatePositionResponse;
  } catch (error: any) {
    throw new Error(error.response.data.error);
  }
};

export const useCreateMarketPosition = (): UseCreateMarketPositionResult => {
  const { loginToken } = useLoginContext();
  return useMutation({
    mutationFn: (params: CreateMarketPositionParams) => createMarketPosition(loginToken, params),
  });
};
