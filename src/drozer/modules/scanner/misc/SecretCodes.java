import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

import android.app.Application;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.AssetManager;
import android.content.res.XmlResourceParser;

public class SecretCodes
{	

	public static String[] find(Application ctx, String pkg) throws NameNotFoundException, IOException, XmlPullParserException {
    AssetManager am = ctx.createPackageContext(pkg, 0).getAssets();
    XmlResourceParser xml = am.openXmlResourceParser("AndroidManifest.xml");

    List<String> codes = new ArrayList<String>();
        
    while(xml.next() != XmlPullParser.END_DOCUMENT) {
    	if(xml.getEventType() == XmlPullParser.START_TAG && xml.getName().equals("data")) {
      	if(xml.getAttributeCount() == 2 && xml.getAttributeValue(0).equals("android_secret_code"))
    			codes.add(xml.getAttributeValue(1));
      }
    }
        
    return codes.toArray(new String[codes.size()]);
	}

}
