import { isChrome } from './browsers';

export function preventScrollByWheelClick(el: HTMLElement): void {
  const enum MouseEventButton {
    Left = 0,
    Middle = 1,
    Right = 2,
    Fourth = 3,
    Fifth = 4,
  }

  if (!isChrome()) {
    return;
  }

  el.addEventListener('mousedown', (e: MouseEvent) => {
    if (e.button === MouseEventButton.Middle) {
      // prevent incorrect scrolling event
      e.preventDefault();
      return false;
    }
    return undefined;
  });
}
