ls *.gz | while read IMAGE; do
	echo $IMAGE
        docker load -i $IMAGE
	#filename="${IMAGE//\//-}"
	#filename="${filename//:/-}.docker-image.gz"
	#docker save ${IMAGE} | pigz --stdout --best > $filename
done
