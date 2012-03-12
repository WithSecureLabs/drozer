// License: Refer to the README in the root directory

package com.mwr.mercury;

import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.IBinder;
import android.widget.Toast;

public class ServerService extends Service
{
	private Server server;
	
	public ServerService()
	{
		super();
	}
	
	@Override
	public IBinder onBind(Intent arg0)
	{
		return null;
	}
	
	@Override
	public void onCreate()
	{
		super.onCreate();
		Toast.makeText(this,"Mercury server started", Toast.LENGTH_LONG).show();
	}
	
	@Override
	public void onDestroy()
	{
		super.onDestroy();
		
		//Stop the server
		try
		{
			server.stopServer();
		}
		catch (Exception e) {}
		
		Toast.makeText(this, "Mercury server stopped", Toast.LENGTH_LONG).show();
	}
	
	
	@Override
	public int onStartCommand(Intent intent, int flags, int startId)
	{
		//Get arguments from intent
	    Bundle args = intent.getExtras();
	    Integer port = (Integer) args.get("port");
	    
		//Start the server with specified port and application context
		server = new Server(port, getApplicationContext());
	    server.start();
	    		
	    //If the service dies, restart and re-issue intent to it
	    return START_REDELIVER_INTENT;
	}

	
	
}
