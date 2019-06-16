import oryginalMoment from 'moment'

const timeFormat = 'YYYY-MM-DD HH:mm'
const interval = 30
const minuteHeight = 2

function moment (date) {
  return oryginalMoment(date, timeFormat)
}

export {moment, timeFormat, interval, minuteHeight}
