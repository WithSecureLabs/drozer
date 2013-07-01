import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import android.content.pm.ApplicationInfo;

class Native {

	public static byte[] get(ApplicationInfo application, String library) throws IOException {
		ZipFile zip_file = new ZipFile(application.publicSourceDir);
		Enumeration<? extends ZipEntry> entries = zip_file.entries();

		ZipEntry entry;
		while(entries.hasMoreElements()) {
			entry = entries.nextElement();

			if(entry.getName().equalsIgnoreCase(library)) {
				ByteArrayOutputStream os = new ByteArrayOutputStream();
				InputStream is = zip_file.getInputStream(entry);

				byte[] buf = new byte[1024];
				int count;
				while((count = is.read(buf)) != -1)
					os.write(buf, 0, count);

				return os.toByteArray();
			}
		}

		return null;
	}

	public static String[] list(ApplicationInfo application) throws IOException {
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

