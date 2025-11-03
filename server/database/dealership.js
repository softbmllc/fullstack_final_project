const mongoose = require('mongoose');

const DealershipSchema = new mongoose.Schema({
  id: Number,
  city: String,
  state: String,   // algunos JSON traen "state"
  st: String,      // otros traen "st"
  address: String,
  zip: String,
  lat: Number,
  long: Number,
  short_name: String,
  full_name: String
}, { collection: 'dealerships', strict: false, versionKey: false });

module.exports = mongoose.model('Dealership', DealershipSchema);