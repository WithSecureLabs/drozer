// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.IOException;
import java.net.ServerSocket;

import android.content.Context;
import android.util.Log;

public class Server extends Thread
{
	//Local variables
	private ServerSocket listener = null;
	Context applicationContext;
	
	public static boolean running;
	
	//Constructor - create a listener
    public Server(Integer port, Context ctx)
    {
		super();
		
		//Place context into local variable
		applicationContext = ctx;
		
		//Start the listener
		try
		{
			listener = new ServerSocket(port);
			running = true;
		}
		catch (Exception e) {}
	}
    
    //Handle a connection made to the server
	@Override
	public void run()
	{
		// Debug.startMethodTracing("merc");
		//Open Mercury persistent shell
		Common.mercuryShell = new Shell();
		
		//Keep on accepting connections while running = true
		while(running)
		{
			try
			{
				Log.e("mercury", "Waiting for connections.");
				
			    //Wait for a connection and create a handler for the client
			    new SessionThread(new Session(listener.accept(), applicationContext)).start();
			}
			catch (IOException e)
			{
				Log.e("mercury", e.getMessage());
			}
		}
		// Debug.stopMethodTracing();
	}

	//Stop server
	public void stopServer()
	{
		running = false;
		
		try
		{
			Log.e("mercury", "Listener stopped");
			listener.close();
			
			//Close Mercury persistent shell
			Common.mercuryShell.closeShell();
		}
		catch (IOException e)
		{
			Log.e("mercury", e.getMessage());
		}
	}
	
}
