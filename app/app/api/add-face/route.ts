import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { image, name } = await req.json();
  const response = await fetch('http://127.0.0.1:5000/add-face', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image, name }),
  });
  const result = await response.json();
  return NextResponse.json(result);
}
