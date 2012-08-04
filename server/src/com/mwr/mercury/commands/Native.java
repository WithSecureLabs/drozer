package com.mwr.mercury.commands;

import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

import java.io.IOException;
import java.util.Enumeration;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class Native
{
	public static void info(List<ArgumentWrapper> argsArray, Session currentSession) {
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();
		
		//Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		
		//Get all packages from packagemanager
		List <PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(PackageManager.GET_PERMISSIONS);
		
		//Iterate through packages
		String output_temp = new String();
		ZipFile zipFile;
		boolean native_found;
		for (PackageInfo package_:packages)
		{
			ApplicationInfo app = package_.applicationInfo;
			
			//Apply filter
			if ((app.packageName.toUpperCase().contains(filter.toUpperCase()) || app.processName.toUpperCase().contains(filter.toUpperCase()) || filter == ""))
            {
				native_found = false;
				output_temp = "Package name: " + app.packageName + "\n";
				
				try {
		        	zipFile = new ZipFile(app.publicSourceDir);
			    	   
		        	Enumeration<? extends ZipEntry> entries = zipFile.entries();
			    
		        	ZipEntry entry;
		        	while(entries.hasMoreElements()) {
		        		entry = entries.nextElement();
		        		String name = entry.getName();
			    		   
		        		if(name.endsWith(".so") | name.endsWith(".SO")| name.endsWith(".So") | name.endsWith(".sO")) {
		        			output_temp += "Native lib: " + name + "\n";
		        			native_found = true;
		        		}
		        	}
			    	   
		        	output_temp += "\n";
			    	   
				} catch (IOException e) {
					output_temp += "Error processing package '" + app.packageName + "': " + e.getMessage();
				}
				
				if(native_found) currentSession.send(output_temp, true);
            }
			
		}

		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}
}
