import android.content.Intent;
import android.content.Context;
import android.os.Bundle;
import android.content.BroadcastReceiver;
import android.content.IntentFilter;

public class RegisterReceiver
{
    public static String output = "";

    public String getOutput()
    {
        String temp = RegisterReceiver.output;
        RegisterReceiver.output = "";
        return temp;
    }

    public void register(Context context, IntentFilter intentfilter)
    {

        context.registerReceiver(new BroadcastReceiver()
        {

            @Override
            public void onReceive(Context context, Intent intent)
            {
                RegisterReceiver.output += "Action: " + intent.getAction() + "\n";
                RegisterReceiver.output += "Raw: " + intent.toString() + "\n";

                Bundle bundle = intent.getExtras();

                //Check if bundle is null e.g. am broadcast -a com.test.bla
                if (bundle != null)
                {
                    for (String key : bundle.keySet())
                    {
                        Object value = bundle.get(key);
                        RegisterReceiver.output += "Extra: " + String.format("%s=%s (%s)", key,  
                        value.toString(), value.getClass().getName()) + "\n";
                    }    
                }
                

                RegisterReceiver.output += "\n";
            }
        }, intentfilter);

    }
}
