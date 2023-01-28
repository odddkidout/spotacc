import connectMongo from "../../lib/mongodb";
import acc from "@/models/acc";

export default async (req, res) => {
    const conn = connectMongo();
    if (req.method === 'GET') {
        const facc = await acc.findOne({});
        res.status(200).json({ facc});
    } else if (req.method === 'PUT') {
        const id = req.query;
        const formdata = req.body;
        if ( id && formdata ) {
            await acc.findByIdAndUpdate(id, formdata);
            res.status(200).json({ message: 'Acc updated' });
        } else {
            res.status(400).json({ message: 'Bad request' });
    }
    } else if (req.method === 'POST') {
        const formdata = req.body;
        if ( formdata ) {
            await acc.create(formdata);
            res.status(200).json({ message: 'Acc created' });
        } else {
            res.status(400).json({ message: 'Bad request' });
    }
    res.status(405).json({ message: 'Method not allowed' });
  }
}