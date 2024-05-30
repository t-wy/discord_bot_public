// https://github.com/SonolusHaniwa/sonolus-sirius-engine/blob/master/convert.h#L120
// up to commit 11be3447bb33e1ebe7f3e9d4fa2b11c75cffeefd

string fromSirius(string text, double chartOffset, double bgmOffset = 0) {
    // 谱面读取
    auto lines = explode("\n", text.c_str());
    vector<Note> notes; double speed = 1;
    for (int i = 0; i < lines.size(); i++) {
        char unused = 0;
        Note x; string xx = lines[i];
        auto components = explode(",", xx.c_str());
        if (components.size() < 7) break;
        x.startTime = atof(components[0].c_str()) + chartOffset;
        x.endTime = atof(components[1].c_str());
        if (x.endTime != -1) x.endTime += chartOffset;
        x.type = atoi(components[2].c_str());
        x.leftLane = atoi(components[3].c_str());
        x.laneLength = atoi(components[4].c_str());
        string s = components[5];
        x.scratchLength = atoi(components[6].c_str());
        if (s == "JumpScratch") x.gimmickType = JumpScratch;
        else if (s == "OneDirection") x.gimmickType = OneDirection;
        else if (s == "11") x.gimmickType = Split1;
        else if (s == "12") x.gimmickType = Split2;
        else if (s == "13") x.gimmickType = Split3;
        else if (s == "14") x.gimmickType = Split4;
        else if (s == "15") x.gimmickType = Split5;
        else if (s == "16") x.gimmickType = Split6;
        else x.gimmickType = 0;
        notes.push_back(x);
    } sort(notes.begin(), notes.end(), [&](Note a, Note b){
        if (a.startTime == b.startTime) return a.type < b.type;
        return a.startTime < b.startTime;
    });
    cout << "[INFO] Total Note Number: " << notes.size() << endl;

    // 开始转换
	Json::Value res, single; set<Note> holdEnd;
    map<double, int> SyncLineLeft, SyncLineRight;
    auto addSyncLine = [&](double beat, int leftLane, int laneLength) {
        if (SyncLineLeft.find(beat) == SyncLineLeft.end()) SyncLineLeft[beat] = leftLane;
        else SyncLineLeft[beat] = min(SyncLineLeft[beat], leftLane);
        if (SyncLineRight.find(beat) == SyncLineRight.end()) SyncLineRight[beat] = leftLane + laneLength - 1;
        else SyncLineRight[beat] = max(SyncLineRight[beat], leftLane + laneLength - 1);
    };
	single["archetype"] = "Sirius Initialization"; single["data"].resize(0);
	res.append(single);
	single["archetype"] = "Sirius Input Manager"; single["data"].resize(0);
	res.append(single);
	single["archetype"] = "Sirius Stage"; single["data"].resize(0);
	res.append(single); 
	single["archetype"] = "#BPM_CHANGE";
	single["data"][0]["name"] = "#BEAT"; single["data"][0]["value"] = 0;
	single["data"][1]["name"] = "#BPM"; single["data"][1]["value"] = 60;
	res.append(single); 
    double lastEighthTime[13][13]; int total = 0;
    for (int i = 0; i < 13; i++) for (int j = 0; j < 13; j++) lastEighthTime[i][j] = 0;
    for (int i = 0; i < notes.size(); i++) {
        // 提前处理 Sirius HoldEnd;
        while (holdEnd.size() && (*holdEnd.begin()).endTime <= notes[i].startTime) {
            Note x = *holdEnd.begin(); holdEnd.erase(holdEnd.begin()); Json::Value single;
            if (x.type == Hold || x.type == CriticalHold) {
                single["archetype"] = "Sirius Hold End";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.endTime;
                single["data"][1]["name"] = "stBeat"; single["data"][1]["value"] = x.startTime;
                single["data"][2]["name"] = "lane"; single["data"][2]["value"] = x.leftLane;
                single["data"][3]["name"] = "laneLength"; single["data"][3]["value"] = x.laneLength;
                total++;
            } else {
                single["archetype"] = "Sirius Scratch Hold End";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.endTime;
                single["data"][1]["name"] = "stBeat"; single["data"][1]["value"] = x.startTime;
                single["data"][2]["name"] = "lane"; single["data"][2]["value"] = x.leftLane;
                single["data"][3]["name"] = "laneLength"; single["data"][3]["value"] = x.laneLength;
                single["data"][4]["name"] = "scratchLength"; single["data"][4]["value"] = x.scratchLength;
                total++;
            }
            res.append(single);
			addSyncLine(x.endTime, x.leftLane, x.laneLength);
        }
        // 处理当前 Note
        Note x = notes[i]; Json::Value single;
        single["archetype"] = "";
        switch(x.type) {
            case Normal: {
                single["archetype"] = "Sirius Normal Note";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case Critical: {
                single["archetype"] = "Sirius Critical Note";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case Flick: {
                single["archetype"] = "Sirius Flick Note";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                single["data"][3]["name"] = "scratchLength"; single["data"][3]["value"] = x.scratchLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case HoldStart: {
                single["archetype"] = "Sirius Hold Start";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break; 
            case CriticalHoldStart: {
                single["archetype"] = "Sirius Critical Hold Start";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case ScratchHoldStart: {
                single["archetype"] = "Sirius Scratch Hold Start";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case ScratchCriticalHoldStart: {
                single["archetype"] = "Sirius Critical Scratch Hold Start";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case Hold: case CriticalHold: case ScratchHold: case ScratchCriticalHold: {
                holdEnd.insert(x);
            } break;
            case Sound: case ScratchSound: {
                lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] = x.startTime;
                single["archetype"] = "Sirius Sound";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
				single["data"][3]["name"] = "holdType"; single["data"][3]["value"] = Sound ? Hold : ScratchHold;
                total++;
            } break;
            case SoundPurple: {
                lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] = x.startTime;
                single["archetype"] = "Sirius Scratch Hold End";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
            	single["data"][1]["name"] = "stBeat"; single["data"][1]["value"] = x.startTime;
                single["data"][2]["name"] = "lane"; single["data"][2]["value"] = x.leftLane;
                single["data"][3]["name"] = "laneLength"; single["data"][3]["value"] = x.laneLength;
                single["data"][4]["name"] = "scratchLength"; single["data"][4]["value"] = 0;
                addSyncLine(x.startTime, x.leftLane, x.laneLength);
                total++;
            } break;
            case HoldEighth: {
                if (lastEighthTime[x.leftLane][x.leftLane + x.laneLength - 1] == x.startTime) break;
                single["archetype"] = "Sirius Hold Eighth";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "lane"; single["data"][1]["value"] = x.leftLane;
                single["data"][2]["name"] = "laneLength"; single["data"][2]["value"] = x.laneLength;
                // 历史遗留代码了，这个属性现在应该不需要了 2024.5.27
				single["data"][3]["name"] = "holdType"; single["data"][3]["value"] = 0;
                total++;
            } break;
            case None: {
                single["archetype"] = "Sirius Split Line";
                single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "endBeat"; single["data"][1]["value"] = x.endTime;
                single["data"][2]["name"] = "split"; single["data"][2]["value"] = x.gimmickType - 10;
                single["data"][3]["name"] = "color"; single["data"][3]["value"] = x.scratchLength;
            } break;
            case HiSpeed: {
                single["archetype"] = "#TIMESCALE_CHANGE";
                single["data"][0]["name"] = "#BEAT"; single["data"][0]["value"] = x.startTime;
                single["data"][1]["name"] = "#TIMESCALE"; single["data"][1]["value"] = x.endTime - chartOffset;
            }
        } if (single["archetype"] != "") res.append(single);
        if (single["archetype"] == Json::Value::null) cout << single << endl;
        if ((10 * (i + 1) / notes.size()) != (10 * i / notes.size())) cout << "[INFO] " << 100 * (i + 1) / notes.size() << "% Notes Solved." << endl;
    }

	// 处理完 HoldEnd
	while (holdEnd.size()) {
        Note x = *holdEnd.begin(); holdEnd.erase(holdEnd.begin()); Json::Value single;
        if (x.type == Hold || x.type == CriticalHold) {
            single["archetype"] = "Sirius Hold End";
            single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.endTime;
            single["data"][1]["name"] = "stBeat"; single["data"][1]["value"] = x.startTime;
            single["data"][2]["name"] = "lane"; single["data"][2]["value"] = x.leftLane;
            single["data"][3]["name"] = "laneLength"; single["data"][3]["value"] = x.laneLength;
            total++;
        } else {
            single["archetype"] = "Sirius Scratch Hold End";
            single["data"][0]["name"] = "beat"; single["data"][0]["value"] = x.endTime;
            single["data"][1]["name"] = "stBeat"; single["data"][1]["value"] = x.startTime;
            single["data"][2]["name"] = "lane"; single["data"][2]["value"] = x.leftLane;
            single["data"][3]["name"] = "laneLength"; single["data"][3]["value"] = x.laneLength;
            single["data"][4]["name"] = "scratchLength"; single["data"][4]["value"] = x.scratchLength;
            total++;
        } res.append(single);
        addSyncLine(x.endTime, x.leftLane, x.laneLength);
    }

    cout << "[INFO] Total Note Number: " << total << endl;
    cout << "[INFO] Solving Sync Line..." << endl;

    // 处理同步线
    for (auto v : SyncLineLeft) {
        double beat = v.first; int left = v.second;
        Json::Value single; single["archetype"] = "Sirius Sync Line";
        single["data"][0]["name"] = "beat"; single["data"][0]["value"] = beat;
        single["data"][1]["name"] = "left"; single["data"][1]["value"] = left;
        single["data"][2]["name"] = "right"; single["data"][2]["value"] = SyncLineRight[beat];
        res.append(single);
    }

    cout << "[INFO] Sync Line Solved." << endl;

	Json::Value data;
	data["formatVersion"] = 5;
	data["bgmOffset"] = bgmOffset;
	data["entities"] = res;
	return json_encode(data);
}