// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import connectMongo from "../../lib/mongodb";
import acc from "@/models/acc";




export default async (req, res) => {
  if (req.method === 'GET') {
    const conn = await connectMongo();
    const TotalAcc = await acc.countDocuments({});
    const Alive = await acc.countDocuments({Working: true});
    const InUse = await acc.countDocuments({InUse: true});
    console.log(TotalAcc, Alive, InUse);
    res.status(200).json({ "total": TotalAcc, "alive": Alive, "inuse": InUse});
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}