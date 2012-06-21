package com.mwr.mercury;

import java.io.IOException;
import java.io.Reader;

public class BufferedBracketReader
{
	private char[] buf = null;
	private int pos;
	private int end;
	private Reader in;
	
	public BufferedBracketReader(Reader is) {
		this.in = is;
		this.buf = new char[512];
		pos = 0;
		end = 0;
	}
	
	private int fillbuf() throws IOException {
		/* Set the new position and mark position */
	//	if(in.ready()) {
			int count = in.read(buf, end, buf.length - end);
			if (count != -1) {
				end = count + end;
			} else {
				throw new IOException("disconnected.");
			}
			return count;
		//}
        //return 0;
	}
	
	public String readChunk() throws IOException {
		if(end==pos) fillbuf();
		int p = pos;
		while(p < end) {			
			if(buf[p] == (char)'>') {
				String ret = new String(buf, pos, (p+1) - pos);
				pos = p + 1;
				return ret;
			}
			p += 1;
		}
		String ret = null;
		if(pos != end) {
			ret = new String(buf, pos, (end-pos));
		}
		pos = 0;		
		end = 0;		
		return ret;
	}
	
	public boolean ready() throws IOException {
		return in.ready();
	}

	public void skipWs() throws IOException
	{		
		fillbuf();
		while(pos< end &&(buf[pos] == ' ' || buf[pos] == '\r' || buf[pos] == '\n' ))
			pos ++;
	}
}
