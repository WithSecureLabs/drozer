// License: Refer to the README in the root directory

package com.mwr.mercury;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;
import android.widget.ToggleButton;


public class Main extends Activity 
{
	//Server on/off toggle
	private ToggleButton mToggleButton;
	
	//Server port
    private Integer port = 31415;
    
    //Stop service containing server
    private void stopServerService()
    {    	
    	stopService(new Intent(Main.this, ServerService.class));	
    }
    
    //Start service containing server
    private void startServerService(int port)
    {
    	try
    	{
            //Formulate intent and start server service
            Intent intent = new Intent(Main.this, ServerService.class);
            intent.putExtra("port", port);
            getApplicationContext().startService(intent);
    	}
    	catch (Exception e)
    	{
    		//Log error and turn toggle off
    		Log.e("mercury", e.getMessage());
    		mToggleButton.setChecked(false);
    	}
    	
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        switch (item.getItemId())
        {
            case R.id.about:
            	
            	AlertDialog alertDialog = new AlertDialog.Builder(Main.this).create();
				alertDialog.setTitle("Information");
				
				//Display information about server
		        try
		        {
		        	PackageInfo info = getPackageManager().getPackageInfo(getPackageName(), 0);
					alertDialog.setMessage("Mercury Server v" + info.versionName + "\nMWR InfoSecurity");
					alertDialog.setButton("OK", new DialogInterface.OnClickListener()
					{  
					      public void onClick(DialogInterface dialog, int which)
					      {  
					          return;  
					      } 
				     });
		        
		        }
		        catch (Exception e) {}
				
				alertDialog.show();
            	
            	
            break;
        }
        return true;
    }
    
	
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
                        
        //Assign this variable to toggle switch
        mToggleButton = (ToggleButton) findViewById(R.id.serverToggleBtn);
        
        //Assign state of the toggle button
        mToggleButton.setChecked(Server.running);
        
        //Handle server on/off when toggle is clicked
        mToggleButton.setOnClickListener(new OnClickListener()
        {
			public void onClick(View arg1)
			{
				if(mToggleButton.isChecked())
					startServerService(port);
				else
					stopServerService();
			}
		});
        
        //Assign this variable to MWR labs logo
        ImageView mwrLabsLogo = (ImageView) findViewById(R.id.mercuryImage);
        
        //Set viewing intent for mwr labs site when clicking on logo
        mwrLabsLogo.setOnClickListener(new OnClickListener()
		{
			
			@Override
			public void onClick(View v)
			{
				// TODO Auto-generated method stub
				Intent intent = new Intent();
				intent.setAction(Intent.ACTION_VIEW);
				intent.setData(Uri.parse("http://mwr.to/hglabs"));
				startActivity(intent);
			}
		});
  
        
    }
     
    
}
