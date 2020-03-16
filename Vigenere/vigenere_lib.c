


void encrypt(char* key, int lenKey, char* txt, int lenTxt){//, char* result) {
	int keyPos = 0;

	for (int i = 0; i < lenTxt; i++){
		int keyValue = key[keyPos]-'A';

		int shift = txt[i]+ keyValue;
		if (shift>'Z') {
			shift -= 26;
		}

		txt[i] = (char)shift;

		keyPos++;
		if (keyPos>= lenKey){
			keyPos = 0;
		}
	}

	//result[lenTxt] = "\0";
}