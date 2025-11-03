const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const path = require("path");
const { MongoMemoryServer } = require("mongodb-memory-server");

const Dealership = require("./dealership");
const Review = require("./review");

const app = express();
app.use(express.json());

async function connectMongo() {
  if (process.env.MONGO_URL) {
    await mongoose.connect(process.env.MONGO_URL);
    return;
  }
  const mongod = await MongoMemoryServer.create();
  const uri = mongod.getUri();
  await mongoose.connect(uri);
}

// lee JSON y devuelve SIEMPRE un array plano
function loadList(p) {
  const raw = JSON.parse(fs.readFileSync(p));
  if (Array.isArray(raw)) return raw;
  // soporta {dealerships:[…]} o {reviews:[…]}
  if (Array.isArray(raw.dealerships)) return raw.dealerships;
  if (Array.isArray(raw.reviews)) return raw.reviews;
  return [];
}

async function seedIfEmpty() {
  const dealersCount = await Dealership.countDocuments();
  const reviewsCount = await Review.countDocuments();

  if (!dealersCount) {
    const dealers = loadList(path.join(__dirname, "data/dealerships.json"));
    await Dealership.insertMany(dealers);
  }
  if (!reviewsCount) {
    const reviews = loadList(path.join(__dirname, "data/reviews.json"));
    await Review.insertMany(reviews);
  }
}

// --- ENDPOINTS ---
app.get("/fetchReviews", async (_req, res) => {
  res.json(await Review.find().lean());
});
app.get("/fetchReviews/dealer/:id", async (req, res) => {
  res.json(await Review.find({ dealership: Number(req.params.id) }).lean());
});
app.get("/fetchDealers", async (_req, res) => {
  res.json(await Dealership.find().lean());
});
app.get("/fetchDealers/:state", async (req, res) => {
  res.json(await Dealership.find({ state: req.params.state }).lean());
});
app.get("/fetchDealer/:id", async (req, res) => {
  const doc = await Dealership.findOne({ id: Number(req.params.id) }).lean();
  if (!doc) return res.status(404).json({ error: "Not found" });
  res.json(doc);
});
app.post("/insert_review", async (req, res) => {
  const payload = req.body || {};
  const max = await Review.findOne().sort("-id").lean();
  const nextId = (max?.id || 0) + 1;
  const doc = await Review.create({ id: nextId, ...payload });
  res.status(201).json(doc);
});

(async () => {
  await connectMongo();
  await seedIfEmpty();
  const port = process.env.PORT || 3030;
  app.listen(port, () => console.log(`Node app on :${port}`));
})();
module.exports = app;