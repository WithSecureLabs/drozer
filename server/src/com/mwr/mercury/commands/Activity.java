// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;

import java.util.List;

public class Activity
{
	public static void info(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();
		
		//Iterate through all packages
		List<PackageInfo> packages = currentSession.applicationContext.getPackageManager().getInstalledPackages(0);
        for(PackageInfo pack : packages)
        {
        	//Get activities in package
            ActivityInfo[] activities = null;
            try
            {
            	activities = currentSession.applicationContext.getPackageManager().getPackageInfo(pack.packageName, PackageManager.GET_ACTIVITIES).activities;
            }
            catch (Exception e) {}
            
        	if (activities != null)
			{	
				for (int i = 0; i < activities.length; i++)
				{
					if (activities[i].exported == true)
					{
						boolean filterPresent = filter.length() != 0;
						boolean filterRelevant = pack.packageName.contains(filter) || activities[i].name.contains(filter);
						
						if ((filterPresent && filterRelevant) || !filterPresent)
						{
							currentSession.send("Package name: " + activities[i].packageName + "\n", true);
							currentSession.send("Activity: " + activities[i].name + "\n\n", true);
						}
					}
				}
			}
        }
		
		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}

	public static void start(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());
		
		try
		{
			currentSession.applicationContext.startActivity(intent);
			currentSession.sendFullTransmission("Activity started with " + intent.toString(), "");
		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}

	public static void match(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());

		try
		{
		
			//Get all activities and iterate through them
			List<ResolveInfo> activities = currentSession.applicationContext.getPackageManager().queryIntentActivities(intent, PackageManager.MATCH_DEFAULT_ONLY & PackageManager.GET_ACTIVITIES & PackageManager.GET_INTENT_FILTERS & PackageManager.GET_RESOLVED_FILTER	);

			String returnVal = intent.toString() + ":\n\n";
			
			for (int i = 0; i < activities.size(); i++)
			{

				String activityPackage = activities.get(i).activityInfo.packageName;
				String activityTargetActivity = activities.get(i).activityInfo.name;

				returnVal += "Package name: " + activityPackage + "\n";
				returnVal += "Target activity: " + activityTargetActivity + "\n\n";

			}
			
			currentSession.sendFullTransmission(returnVal.trim(), "");
		
		}
		catch (Exception e)
		{
			currentSession.sendFullTransmission("", e.getMessage());
		}
	}

	public static void launchIntent(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Assign filter if one came in the arguments
		String packageName = Common.getParamString(argsArray, "packageName");
		
		Intent intent = currentSession.applicationContext.getPackageManager().getLaunchIntentForPackage(packageName);
		
		//Send intent back
		if (intent != null)
			currentSession.sendFullTransmission(intent.toString(), "");
		else
			currentSession.sendFullTransmission("", "No intent returned	");
	}

}
