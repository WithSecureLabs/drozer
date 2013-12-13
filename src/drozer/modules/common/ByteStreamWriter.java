import java.io.OutputStream;
import java.io.IOException;

public class ByteStreamWriter {

  public static boolean writeHexStream(OutputStream stream, String hex_stream) throws IOException {
    int len = hex_stream.length();
    byte[] byte_stream = new byte[len / 2];

    for(int i=0; i<len; i+=2)
      byte_stream[i/2] = (byte)((Character.digit(hex_stream.charAt(i), 16) << 4) + Character.digit(hex_stream.charAt(i+1), 16));

    stream.write(byte_stream, 0, byte_stream.length);

    return true;
  }

}
