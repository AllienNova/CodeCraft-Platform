import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
              About CodeCraft
            </span>
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed">
            We're on a mission to transform how children learn programming - making it magical, 
            engaging, and accessible for every young mind ready to shape the future.
          </p>
        </div>
      </section>

      {/* Mission, Vision, Values */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Mission */}
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-6">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Our Mission</h3>
              <p className="text-gray-600 leading-relaxed">
                To democratize coding education by creating magical, age-appropriate learning experiences 
                that transform children into confident programmers while fostering creativity, critical thinking, 
                and problem-solving skills essential for the digital future.
              </p>
            </div>

            {/* Vision */}
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mb-6">
                <span className="text-2xl">🔮</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Our Vision</h3>
              <p className="text-gray-600 leading-relaxed">
                A world where every child, regardless of background, has access to world-class coding education 
                that feels like play but builds real skills. We envision a generation of confident, creative 
                digital natives ready to solve tomorrow's challenges.
              </p>
            </div>

            {/* Values */}
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mb-6">
                <span className="text-2xl">💎</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Our Values</h3>
              <p className="text-gray-600 leading-relaxed">
                <strong>Safety First:</strong> COPPA+ compliant platform with comprehensive parental controls.<br/>
                <strong>Inclusive Learning:</strong> Accessible design for all abilities and backgrounds.<br/>
                <strong>Joyful Discovery:</strong> Learning should feel magical and exciting.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Our Story
            </span>
          </h2>
          <div className="prose prose-lg mx-auto text-gray-700">
            <p className="text-xl leading-relaxed mb-6">
              CodeCraft was born from a simple observation: traditional coding education wasn't working for children. 
              Complex syntax, boring tutorials, and one-size-fits-all approaches were leaving young minds frustrated 
              and disengaged.
            </p>
            <p className="text-lg leading-relaxed mb-6">
              Our founder, a parent of three daughters aged 5, 9, and 10, experienced this firsthand. Watching his 
              children struggle with existing coding platforms, he envisioned something different - a platform that 
              would adapt to each child's age, learning style, and interests.
            </p>
            <p className="text-lg leading-relaxed mb-6">
              Working with child development experts, educators, and professional developers, we created three distinct 
              learning environments: the Magic Workshop for young explorers, the Innovation Lab for creative builders, 
              and the Professional Studio for aspiring developers.
            </p>
            <p className="text-lg leading-relaxed">
              Today, over 2,847 families trust CodeCraft to nurture their children's coding journey. Every magical 
              adventure, every app built, every line of code written brings us closer to our vision of a world where 
              every child can confidently create with technology.
            </p>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Meet Our Team
            </span>
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Team Member 1 */}
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-3xl text-white">👨‍💻</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Alex Chen</h3>
              <p className="text-purple-600 font-semibold mb-4">Founder & CEO</p>
              <p className="text-gray-600">
                Former Google engineer and father of three. Passionate about making coding accessible 
                and enjoyable for all children.
              </p>
            </div>

            {/* Team Member 2 */}
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-3xl text-white">👩‍🎓</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Dr. Sarah Martinez</h3>
              <p className="text-blue-600 font-semibold mb-4">Head of Education</p>
              <p className="text-gray-600">
                Child development expert with 15+ years in educational technology. 
                Designs age-appropriate learning experiences.
              </p>
            </div>

            {/* Team Member 3 */}
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full mx-auto mb-6 flex items-center justify-center">
                <span className="text-3xl text-white">🎨</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Maya Patel</h3>
              <p className="text-green-600 font-semibold mb-4">Creative Director</p>
              <p className="text-gray-600">
                Award-winning designer specializing in child-friendly interfaces. 
                Creates the magical experiences that make learning irresistible.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Stats */}
      <section className="py-16 px-4 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-12">Our Impact</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">2,847+</div>
              <div className="text-purple-200">Families Joined</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">15,000+</div>
              <div className="text-purple-200">Apps Created</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">95%</div>
              <div className="text-purple-200">Parent Satisfaction</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">50+</div>
              <div className="text-purple-200">Countries Reached</div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Join Our Mission
            </span>
          </h2>
          <p className="text-xl text-gray-700 mb-8">
            Be part of the movement transforming how children learn to code. 
            Together, we're building the next generation of confident creators.
          </p>
          <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105">
            Start Your Child's Journey
          </button>
        </div>
      </section>
    </div>
  );
};

export default About;

