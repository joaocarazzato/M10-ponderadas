import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart';


class PaginaCamera extends StatefulWidget {
  const PaginaCamera({super.key});

  @override
  State<PaginaCamera> createState() => _PaginaCamera();

  }

class _PaginaCamera extends State<PaginaCamera> {

  File? pickedFile;


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Mudança de imagem"),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        ),
      body: 
        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (pickedFile != null)
              Expanded(
              child : Container(
              child: Image.file(
                pickedFile!,
                fit: BoxFit.contain,
              ),
             ),
            ),
              ElevatedButton(
                onPressed: () => _selectAndShareImage(context),
                child: Text('Selecione sua imagem'),
              ),
            ],
          ),
        ),
    );
  }

  Future<void> _selectAndShareImage(BuildContext context) async {
    final picker = ImagePicker();
    XFile? file = await picker.pickImage(source: ImageSource.gallery);
    if (file != null) {
      setState(() {
        pickedFile = File(file.path);
      });
    }
    }
}