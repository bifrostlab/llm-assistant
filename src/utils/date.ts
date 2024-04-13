import { getUnixTime } from 'date-fns';

export function getCurrentUnixTime(): number {
  return getUnixTime(new Date());
}
