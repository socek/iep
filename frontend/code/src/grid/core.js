import moment from 'moment'

export default {
  interval: 30,
  minuteHeight: 2,
  timeFormat: 'YYYY-MM-DD HH:mm',
  start: moment('2017-02-20 10:00', this.timeFormat),
  end: moment('2017-02-22 14:00', this.timeFormat),
  timestamps: undefined,
  rooms: undefined,

  moment: function (date) {
    return moment(date, this.timeFormat)
  },

  createTimestamps: function () {
    this.timestamps = []
    let current = this.start.clone()

    while (current <= this.end) {
      this.timestamps.push(current.format(this.timeFormat))
      current = current.add(this.interval, 'm')
    }
  },

  createRooms: function () {
    this.rooms = [
      'Pokój A',
      'Pokój B',
      'Pokój C',
      'Pokój D'
    ]
  }
}
