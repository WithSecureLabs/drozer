// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ServiceInfo;

import java.util.List;

public class Broadcast
{
	public static void info(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		//Assign filter and permissions if they came in the arguments
		String filter = Common.getParamString(argsArray, "filter");
		String permissions = Common.getParamString(argsArray, "permissions");
		
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();
		
		//Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext.getPackageManager();
		List <PackageInfo> packages = pm.getInstalledPackages(PackageManager.GET_RECEIVERS | PackageManager.GET_PERMISSIONS);
		
		
		//Iterate through packages
		for (PackageInfo package_:packages)
		{
			ActivityInfo[] receivers = package_.receivers;			
			
			if (receivers != null)
			{	
				for (int i = 0; i < receivers.length; i++)
				{							
					boolean relevantFilter = false;
					boolean relevantPermissions = false;
					boolean noFilters = false;
					boolean bothFiltersRelevant = false;
					
					//Check if a filter was used
					if (filter.length() > 0)
						relevantFilter = package_.packageName.contains(filter) || receivers[i].name.contains(filter);
					
					//Check if a permission filter was used
					try
					{
						if (permissions.length() > 0)
						{
							if (permissions.toUpperCase().equals("NULL"))
								relevantPermissions = (receivers[i].permission == null);
							else
								relevantPermissions = receivers[i].permission.contains(permissions);
						}
					} catch (Throwable t) {}
					
					//Check if no parameters were given
					if (filter.length() == 0 && permissions.length() == 0)
						noFilters = true;
					
					boolean bothFiltersPresent = false;
					if ((filter != "") && (permissions != ""))
						bothFiltersPresent = true;
					
					if (bothFiltersPresent && relevantFilter && relevantPermissions)
						bothFiltersRelevant = true;
					
					//Apply filter and only look @ exported providers
					if (((bothFiltersPresent && bothFiltersRelevant) || (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters)) && receivers[i].exported)
					{
						currentSession.send("Package name: " + receivers[i].packageName + "\n", true);
						currentSession.send("Receiver: " + receivers[i].name + "\n", true);
						currentSession.send("Required Permission: " + receivers[i].permission + "\n\n", true);
					}
				}
			}
		}

		currentSession.endData();
		currentSession.noError();
		currentSession.endResponse();
		currentSession.endTransmission();
	}

	public static void send(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Parse intent
		Intent intent = Common.parseIntentGeneric(argsArray, new Intent());

		try
		{
			currentSession.applicationContext.sendBroadcast(intent);
			currentSession.sendFullTransmission(
					"Broadcast sent with " + intent.toString(), "");
		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}

}
