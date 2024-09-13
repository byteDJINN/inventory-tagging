// gpt-4o-mini image recognition
import OpenAI from 'openai';
import { OPENAI_API_KEY } from './.env';

const client = new OpenAI({
    apiKey: OPENAI_API_KEY
});

interface Item {
    name: string;
    description: string;
}

export async function recognizeItem(base64Image: string): Promise<Item> {
    const response = await client.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: "You are an object recognition model used for store inventory management. Respond with a JSON object containing a 'name' and 'description' field."
            },
            {
                role: "user",
                content: [
                    {
                        type: "text",
                        text: "Attached is an image. Provide a four-word name and visual description in JSON format."
                    },
                    {
                        type: "image_url",
                        image_url: { url: `data:image/jpeg;base64,${base64Image}` }
                    }
                ]
            }
        ],
        max_tokens: 300,
        response_format: { type: "json_object" }
    });

    const item: Item = JSON.parse(response.choices[0].message.content || '{"name": "", "description": ""}');
    return item;
}