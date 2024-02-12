import java.io.IOException;

import android.content.res.XmlResourceParser;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

public class XmlAssetReader {

  public static String read(XmlResourceParser xml) {
    StringBuilder output = new StringBuilder();

    try {
      while (xml.next() != XmlPullParser.END_DOCUMENT) {
        switch (xml.getEventType()) {
        case XmlPullParser.START_TAG:
          output.append("<");
          output.append(xml.getName());
          for(int i=0; i<xml.getAttributeCount(); i++) {
            output.append(" ");
            output.append(xml.getAttributeName(i));
            output.append("=\"");
            output.append(xml.getAttributeValue(i));
            output.append("\"");
          }
          output.append(">\n");
          break;

        case XmlPullParser.END_TAG:
          output.append("</");
          output.append(xml.getName());
          output.append(">\n");
          break;

        case XmlPullParser.TEXT:
          output.append(xml.getText());
          output.append("\n");
          break;
        
        default:
          break;
        }
      }
    }
    catch(IOException e) {
      return null;
    }
    catch(XmlPullParserException e) {
      return null;
    }

    return output.toString();
  }

}
