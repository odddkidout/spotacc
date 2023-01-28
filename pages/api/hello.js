// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { writeFileSync } from 'fs';



export default async (req, res) => {
  if (req.method === 'POST') {
    console.log(req.body['name']);
    const { mongoCluster, mongoUsername, mongoPassword, databaseName } = req.body;
    writeFileSync('.env.local', `MONGO_URI="mongodb+srv://${mongoUsername}:${mongoPassword}@${mongoCluster}.mongodb.net/?retryWrites=true&w=majority"\nMONGO_DB="${databaseName}"`);
    res.status(200).json({ message: 'MongoDB credentials saved to .env file' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}