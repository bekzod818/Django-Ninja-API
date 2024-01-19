async function getDevice(slug) {
    const endpoint = 'http://127.0.0.1:8000/api/v1/devices/${slug}'
    const res = await fetch(endpoint, {cache: 'no-store'})

    if (!res.ok) {
        // This will activate the closest `error.js` Error Boundary
        throw new Error("Failed to fetch data")
    }

    return res.json()
}

export default async function Device({params}) {
    return (
        <div className="flex flex-col items-center mt-2">
            <h1 className="text-4xl">Device: {params.slug}</h1>
        </div>
    )
}