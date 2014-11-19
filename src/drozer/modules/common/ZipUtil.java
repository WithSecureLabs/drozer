import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ZipUtil {

  private static final int BUFFER_SIZE = 4096;

  public static File unzip(String target, String zip_file, String destination) throws IOException {
    ZipEntry zip_entry;
    ZipInputStream zip_stream = new ZipInputStream(new BufferedInputStream(new FileInputStream(zip_file)));
    File file = null;
    
    while((zip_entry = zip_stream.getNextEntry()) != null) {
      String zipEntryName = zip_entry.getName();

      if (zip_entry.getName().toUpperCase().equals(target.toUpperCase())) {
        file = new File(destination, System.currentTimeMillis() + ".tmp");

        BufferedOutputStream file_stream = new BufferedOutputStream(new FileOutputStream(file), BUFFER_SIZE);
        
        byte buf[] = new byte[BUFFER_SIZE];
        int count;
        while((count = zip_stream.read(buf, 0, BUFFER_SIZE)) != -1)
          file_stream.write(buf, 0, count);

        file_stream.flush();
        file_stream.close();
        
        break;
      }
    }

    zip_stream.close();

    return file;
  }

}
