import 'package:flutter_secure_storage/flutter_secure_storage.dart';

AndroidOptions _getAndroidOptions() => const AndroidOptions(
        encryptedSharedPreferences: true,
      );


class StorageApi {
  // Obtain shared preferences.
  final storage = FlutterSecureStorage(aOptions: _getAndroidOptions());

  Future<void> saveId(int mainId) async {
    print("Id chegou: $mainId");
    await storage.write(key: "id", value: mainId.toString());
  }

  Future getId() async {
    String? mainId = await storage.read(key: 'id');
    print("Pegando Id: $mainId");
    return mainId;
  }
}