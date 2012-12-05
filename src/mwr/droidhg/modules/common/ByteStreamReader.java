import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.IOException;

import android.util.Base64;

public class ByteStreamReader {

	public static byte[] read(InputStream stream) throws IOException {
		ByteArrayOutputStream output = new ByteArrayOutputStream();

		int c = 0;

		while (c > -1) {
			byte[] buf = new byte[4096];
			c = stream.read(buf);

			if (c > 0)
				output.write(buf, 0, c);
		}

		return output.toByteArray();
	}

	public static byte[] read(InputStream stream, int offset, int count) throws IOException {
		ByteArrayOutputStream output = new ByteArrayOutputStream();

		int c = 0;
		int t = 0;

		while (c > -1 && t < count) {
			byte[] buf = new byte[count];
			c = stream.read(buf, offset + t, count - t);

			if (c > 0) {
				output.write(buf, 0, c);
				
				t += c;
			}
		}

		return output.toByteArray();
	}

}
