import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { image } = await req.json();
    const response = await fetch('http://127.0.0.1:5000/recognize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });
    if (!response.ok) {
      const text = await response.text();
      return NextResponse.json({ name: 'Error', error: text }, { status: response.status });
    }
    const result = await response.json();
    return NextResponse.json({ name: result.name });
  } catch (error: any) {
    return NextResponse.json({ name: 'Error', error: error.message }, { status: 500 });
  }
}
