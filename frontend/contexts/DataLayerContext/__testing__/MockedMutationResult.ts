import { UseMutationResult } from '@tanstack/react-query';

export function MockedMutationResult<PropsType, ReturnType>(
  propsValue: PropsType,
  returnValue: ReturnType
) {
  return {
    data: returnValue,
    isError: false,
    variables: propsValue,
    error: null,
    isPending: false,
    isIdle: false,
    isPaused: false,
    isSuccess: true,
    status: 'success',
    failureCount: 0,
    failureReason: null,
    mutateAsync: jest.fn().mockReturnValue(Promise.resolve(returnValue)),
    mutate: jest.fn(),
    reset: jest.fn(),
    context: null,
    submittedAt: 0,
  } as UseMutationResult<ReturnType, Error, PropsType, unknown>;
}
