import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class FileUtil {

  private static final int BUFFER_SIZE = 4096;

  public static String md5sum(File file) throws IOException, NoSuchAlgorithmException {
    MessageDigest digest = MessageDigest.getInstance("MD5");
    FileInputStream file_stream = new FileInputStream(file);

    byte[] buf = new byte[BUFFER_SIZE];
    int count = 0;
    while((count = file_stream.read(buf, 0, BUFFER_SIZE)) != -1)
      digest.update(buf, 0, count);

    return new BigInteger(1, digest.digest()).toString(16);
  }

  public static StringBuffer read(File file) throws IOException {
    StringBuffer data = new StringBuffer();
    BufferedInputStream file_stream = new BufferedInputStream(new FileInputStream(file));

    byte[] buf = new byte[BUFFER_SIZE];
    int count;
    while((count = file_stream.read(buf, 0, BUFFER_SIZE)) != -1)
      data.append(new String(buf));

    file_stream.close();

    //return file.toString();
    return data;
  }

}
