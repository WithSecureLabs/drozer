import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import android.content.pm.ApplicationInfo;

class Native {

  public static String[] libraries(ApplicationInfo application) throws IOException {
    ArrayList<String> libraries = new ArrayList<String>();

    ZipFile zip_file = new ZipFile(application.publicSourceDir);

    Enumeration<? extends ZipEntry> entries = zip_file.entries();

    ZipEntry entry;
    while(entries.hasMoreElements()) {
      entry = entries.nextElement();
      String name = entry.getName();
      if(name.toUpperCase().endsWith(".SO"))
        libraries.add(name);
    }

    return libraries.toArray(new String[libraries.size()]);
  }

}
