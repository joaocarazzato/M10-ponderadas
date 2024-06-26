import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_app/main.dart';


@pragma('vm:entry-point')
Future<void> handleBackgroundMessage(RemoteMessage message) async {
  print("Title ${message.notification?.title}");
  print("Body ${message.notification?.body}");
  print("Payload ${message.data}");

}

class FirebaseApi {
  final _firebaseMessaging = FirebaseMessaging.instance;

  void handleMessage(RemoteMessage? message) {
    if (message == null) return;
    print("message: ${message.data['data']}");
    navigatorKey.currentState?.pushNamed(
      '/camera',
      arguments: message,
    );
    
  }

  Future initPushNotifications() async {
    await FirebaseMessaging.instance.setForegroundNotificationPresentationOptions(
      alert: true,
      badge: true,
      sound: true,
    );

    FirebaseMessaging.instance.getInitialMessage().then(handleMessage);
    FirebaseMessaging.onMessageOpenedApp.listen(handleMessage);
    FirebaseMessaging.onBackgroundMessage(handleBackgroundMessage);
  }

  Future initNotifications() async {
    await _firebaseMessaging.requestPermission();
    final fCMToken = await _firebaseMessaging.getToken();
    print("Token: $fCMToken");
    initPushNotifications();
    return fCMToken;
  }
}