import { UseMutationResult } from '@tanstack/react-query';

export function MockedMutationResultError<PropsType, ReturnType, ErrorType>(
  propsValue: PropsType,
  returnValue: ReturnType,
  errorValue: ErrorType
) {
  return {
    data: returnValue,
    isError: false,
    variables: propsValue,
    error: errorValue,
    isPending: false,
    isIdle: false,
    isPaused: false,
    isSuccess: true,
    status: 'success',
    failureCount: 1,
    failureReason: errorValue,
    mutateAsync: jest.fn().mockReturnValue(Promise.reject(errorValue)),
    mutate: jest.fn(),
    reset: jest.fn(),
    context: null,
    submittedAt: 0,
  } as UseMutationResult<ReturnType, ErrorType, PropsType, unknown>;
}
