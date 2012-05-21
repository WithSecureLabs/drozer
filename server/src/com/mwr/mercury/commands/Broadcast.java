package com.mwr.mercury.commands;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Session;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;

import java.util.List;

public class Broadcast
{
	public static void info(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Assign filter if one came in the arguments
		String filter = Common.getParamString(argsArray, "filter");

		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();

		// Get all packages from packagemanager
		PackageManager pm = currentSession.applicationContext
				.getPackageManager();
		List<PackageInfo> packages = pm
				.getInstalledPackages(PackageManager.GET_RECEIVERS
						| PackageManager.GET_PERMISSIONS);

		// Iterate through packages
		for (PackageInfo package_ : packages)
		{

			ActivityInfo[] receivers = package_.receivers;

			if (receivers != null)
			{
				for (int i = 0; i < receivers.length; i++)
				{
					if (receivers[i].exported == true)
					{
						boolean filterPresent = filter.length() != 0;
						boolean filterRelevant = package_.packageName
								.contains(filter)
								|| receivers[i].name.contains(filter);

						if ((filterPresent && filterRelevant) || !filterPresent)
						{
							currentSession.send("Package name: "
									+ receivers[i].packageName + "\n", true);
							currentSession.send("Receiver: "
									+ receivers[i].name + "\n\n", true);
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
