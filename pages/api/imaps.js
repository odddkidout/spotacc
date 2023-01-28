// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { writeFileSync } from 'fs';



export default async (req, res) => {
  if (req.method === 'POST') {
    console.log(req.body);
    const { imapUsername, imapPassword, imapHost } = req.body;
    writeFileSync('imap.txt', `imapUsername:${imapUsername}\nimapPassword:${imapPassword}\nimapHost:${imapHost}`);
    res.status(200).json({ message: 'Imap credentials saved to .env file' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}