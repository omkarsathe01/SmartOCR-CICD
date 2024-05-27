def textfromdoc():
    # try:
    document = request.files['doc']
    doc_type = request.form.get('doc_type')
    if not document:
        response = {
            "success": "false",
            "status": "Document not found"
        }
        return response
    keys = request.args.getlist('key')
    filename_complete_name = secure_filename(document.filename)
    filename_front_name = filename_complete_name.split(".")[0]
    idx = len(filename_complete_name.split('.')) - 1
    filename_ext = filename_complete_name.split(".")[idx]

    if filename_ext == "pdf":
        images = convert_from_bytes(document.read())
        image_path = []
        # Save the images
        for image in images:
            filename_new_name = filename_front_name + str(id_generator()) + "." + "png"
            image.save(os.path.join(uploaded_folder, filename_new_name))
            img_path = os.path.join(uploaded_folder, filename_new_name)
            image_path.append(img_path)
    else:
        filename_new_name = filename_front_name + str(id_generator()) + "." + filename_ext
        document.save(os.path.join(uploaded_folder, filename_new_name))
        image_path = [os.path.join(uploaded_folder, filename_new_name)]

    data = func(image_path, keys, doc_type)
    end_time = time.time()
    logging.info(end_time)
    elapsed_time = end_time - start_time
    logging.info(elapsed_time)
    return data