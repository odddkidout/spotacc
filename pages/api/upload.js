export default async (req, res) => {
  if (req.method === 'POST') {
    console.log(req.body);
    res.status(200).json({ message: 'Accs added' });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}